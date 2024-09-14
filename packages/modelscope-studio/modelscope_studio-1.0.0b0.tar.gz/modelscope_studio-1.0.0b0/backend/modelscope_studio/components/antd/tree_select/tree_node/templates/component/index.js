function Y(e) {
  const {
    gradio: t,
    _internal: i,
    ...n
  } = e;
  return Object.keys(i).reduce((l, s) => {
    const o = s.match(/bind_(.+)_event/);
    if (o) {
      const c = o[1], u = c.split("_"), a = (...m) => {
        const y = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
          type: f.type,
          detail: f.detail,
          timestamp: f.timeStamp,
          clientX: f.clientX,
          clientY: f.clientY,
          targetId: f.target.id,
          targetClassName: f.target.className,
          altKey: f.altKey,
          ctrlKey: f.ctrlKey,
          shiftKey: f.shiftKey,
          metaKey: f.metaKey
        } : f);
        return t.dispatch(c.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: y,
          component: n
        });
      };
      if (u.length > 1) {
        let m = {
          ...n.props[u[0]] || {}
        };
        l[u[0]] = m;
        for (let f = 1; f < u.length - 1; f++) {
          const h = {
            ...n.props[u[f]] || {}
          };
          m[u[f]] = h, m = h;
        }
        const y = u[u.length - 1];
        return m[`on${y.slice(0, 1).toUpperCase()}${y.slice(1)}`] = a, l;
      }
      const _ = u[0];
      l[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return l;
  }, {});
}
function k() {
}
function D(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function L(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return k;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(e) {
  let t;
  return L(e, (i) => t = i)(), t;
}
const p = [];
function b(e, t = k) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function l(c) {
    if (D(e, c) && (e = c, i)) {
      const u = !p.length;
      for (const a of n)
        a[1](), p.push(a, e);
      if (u) {
        for (let a = 0; a < p.length; a += 2)
          p[a][0](p[a + 1]);
        p.length = 0;
      }
    }
  }
  function s(c) {
    l(c(e));
  }
  function o(c, u = k) {
    const a = [c, u];
    return n.add(a), n.size === 1 && (i = t(l, s) || k), c(e), () => {
      n.delete(a), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: l,
    update: s,
    subscribe: o
  };
}
const {
  getContext: M,
  setContext: E
} = window.__gradio__svelte__internal, Z = "$$ms-gr-antd-slots-key";
function B() {
  const e = b({});
  return E(Z, e);
}
const G = "$$ms-gr-antd-context-key";
function H(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = z(), i = T({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((u) => {
    i.slotKey.set(u);
  }), J();
  const n = M(G), l = ((c = g(n)) == null ? void 0 : c.as_item) || e.as_item, s = n ? l ? g(n)[l] : g(n) : {}, o = b({
    ...e,
    ...s
  });
  return n ? (n.subscribe((u) => {
    const {
      as_item: a
    } = g(o);
    a && (u = u[a]), o.update((_) => ({
      ..._,
      ...u
    }));
  }), [o, (u) => {
    const a = u.as_item ? g(n)[u.as_item] : g(n);
    return o.set({
      ...u,
      ...a
    });
  }]) : [o, (u) => {
    o.set(u);
  }];
}
const V = "$$ms-gr-antd-slot-key";
function J() {
  E(V, b(void 0));
}
function z() {
  return M(V);
}
const Q = "$$ms-gr-antd-component-slot-context-key";
function T({
  slot: e,
  index: t,
  subIndex: i
}) {
  return E(Q, {
    slotKey: b(e),
    slotIndex: b(t),
    subSlotIndex: b(i)
  });
}
function W(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var R = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function i() {
      for (var s = "", o = 0; o < arguments.length; o++) {
        var c = arguments[o];
        c && (s = l(s, n(c)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return i.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var o = "";
      for (var c in s)
        t.call(s, c) && s[c] && (o = l(o, c));
      return o;
    }
    function l(s, o) {
      return o ? s ? s + " " + o : s + o : s;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(R);
var $ = R.exports;
const tt = /* @__PURE__ */ W($), {
  getContext: et,
  setContext: nt
} = window.__gradio__svelte__internal;
function st(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function i(l = ["default"]) {
    const s = l.reduce((o, c) => (o[c] = b([]), o), {});
    return nt(t, {
      itemsMap: s,
      allowedSlots: l
    }), s;
  }
  function n() {
    const {
      itemsMap: l,
      allowedSlots: s
    } = et(t);
    return function(o, c, u) {
      l && (o ? l[o].update((a) => {
        const _ = [...a];
        return s.includes(o) ? _[c] = u : _[c] = void 0, _;
      }) : s.includes("default") && l.default.update((a) => {
        const _ = [...a];
        return _[c] = u, _;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: n
  };
}
const {
  getItems: it,
  getSetItemFn: lt
} = st("tree-select"), {
  SvelteComponent: ot,
  check_outros: rt,
  component_subscribe: x,
  create_slot: ct,
  detach: ut,
  empty: ft,
  flush: d,
  get_all_dirty_from_scope: at,
  get_slot_changes: _t,
  group_outros: mt,
  init: dt,
  insert: yt,
  safe_not_equal: bt,
  transition_in: j,
  transition_out: P,
  update_slot_base: ht
} = window.__gradio__svelte__internal;
function F(e) {
  let t;
  const i = (
    /*#slots*/
    e[21].default
  ), n = ct(
    i,
    e,
    /*$$scope*/
    e[20],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(l, s) {
      n && n.m(l, s), t = !0;
    },
    p(l, s) {
      n && n.p && (!t || s & /*$$scope*/
      1048576) && ht(
        n,
        i,
        l,
        /*$$scope*/
        l[20],
        t ? _t(
          i,
          /*$$scope*/
          l[20],
          s,
          null
        ) : at(
          /*$$scope*/
          l[20]
        ),
        null
      );
    },
    i(l) {
      t || (j(n, l), t = !0);
    },
    o(l) {
      P(n, l), t = !1;
    },
    d(l) {
      n && n.d(l);
    }
  };
}
function gt(e) {
  let t, i, n = (
    /*$mergedProps*/
    e[0].visible && F(e)
  );
  return {
    c() {
      n && n.c(), t = ft();
    },
    m(l, s) {
      n && n.m(l, s), yt(l, t, s), i = !0;
    },
    p(l, [s]) {
      /*$mergedProps*/
      l[0].visible ? n ? (n.p(l, s), s & /*$mergedProps*/
      1 && j(n, 1)) : (n = F(l), n.c(), j(n, 1), n.m(t.parentNode, t)) : n && (mt(), P(n, 1, 1, () => {
        n = null;
      }), rt());
    },
    i(l) {
      i || (j(n), i = !0);
    },
    o(l) {
      P(n), i = !1;
    },
    d(l) {
      l && ut(t), n && n.d(l);
    }
  };
}
function pt(e, t, i) {
  let n, l, s, o, c, {
    $$slots: u = {},
    $$scope: a
  } = t, {
    gradio: _
  } = t, {
    props: m = {}
  } = t;
  const y = b(m);
  x(e, y, (r) => i(19, c = r));
  let {
    _internal: f = {}
  } = t, {
    as_item: h
  } = t, {
    value: C
  } = t, {
    title: K
  } = t, {
    visible: S = !0
  } = t, {
    elem_id: v = ""
  } = t, {
    elem_classes: w = []
  } = t, {
    elem_style: I = {}
  } = t;
  const N = z();
  x(e, N, (r) => i(18, o = r));
  const [O, U] = H({
    gradio: _,
    props: c,
    _internal: f,
    visible: S,
    elem_id: v,
    elem_classes: w,
    elem_style: I,
    as_item: h,
    value: C,
    title: K
  });
  x(e, O, (r) => i(0, s = r));
  const q = B();
  x(e, q, (r) => i(17, l = r));
  const X = lt(), {
    default: A
  } = it();
  return x(e, A, (r) => i(16, n = r)), e.$$set = (r) => {
    "gradio" in r && i(6, _ = r.gradio), "props" in r && i(7, m = r.props), "_internal" in r && i(8, f = r._internal), "as_item" in r && i(9, h = r.as_item), "value" in r && i(10, C = r.value), "title" in r && i(11, K = r.title), "visible" in r && i(12, S = r.visible), "elem_id" in r && i(13, v = r.elem_id), "elem_classes" in r && i(14, w = r.elem_classes), "elem_style" in r && i(15, I = r.elem_style), "$$scope" in r && i(20, a = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    128 && y.update((r) => ({
      ...r,
      ...m
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, title*/
    589632 && U({
      gradio: _,
      props: c,
      _internal: f,
      visible: S,
      elem_id: v,
      elem_classes: w,
      elem_style: I,
      as_item: h,
      value: C,
      title: K
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots, $items*/
    458753 && X(o, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: tt(s.elem_classes, "ms-gr-antd-tree-select-node"),
        id: s.elem_id,
        title: s.title,
        value: s.value,
        ...s.props,
        ...Y(s)
      },
      slots: l,
      children: n.length > 0 ? n : void 0
    });
  }, [s, y, N, O, q, A, _, m, f, h, C, K, S, v, w, I, n, l, o, c, a, u];
}
class xt extends ot {
  constructor(t) {
    super(), dt(this, t, pt, gt, bt, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      value: 10,
      title: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), d();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), d();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), d();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), d();
  }
  get value() {
    return this.$$.ctx[10];
  }
  set value(t) {
    this.$$set({
      value: t
    }), d();
  }
  get title() {
    return this.$$.ctx[11];
  }
  set title(t) {
    this.$$set({
      title: t
    }), d();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), d();
  }
}
export {
  xt as default
};
