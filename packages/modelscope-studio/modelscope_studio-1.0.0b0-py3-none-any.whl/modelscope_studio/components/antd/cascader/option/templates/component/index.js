function Y(t) {
  const {
    gradio: e,
    _internal: i,
    ...n
  } = t;
  return Object.keys(i).reduce((l, s) => {
    const o = s.match(/bind_(.+)_event/);
    if (o) {
      const c = o[1], u = c.split("_"), f = (...m) => {
        const b = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
          type: a.type,
          detail: a.detail,
          timestamp: a.timeStamp,
          clientX: a.clientX,
          clientY: a.clientY,
          targetId: a.target.id,
          targetClassName: a.target.className,
          altKey: a.altKey,
          ctrlKey: a.ctrlKey,
          shiftKey: a.shiftKey,
          metaKey: a.metaKey
        } : a);
        return e.dispatch(c.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (u.length > 1) {
        let m = {
          ...n.props[u[0]] || {}
        };
        l[u[0]] = m;
        for (let a = 1; a < u.length - 1; a++) {
          const h = {
            ...n.props[u[a]] || {}
          };
          m[u[a]] = h, m = h;
        }
        const b = u[u.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, l;
      }
      const _ = u[0];
      l[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return l;
  }, {});
}
function k() {
}
function D(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function L(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return k;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(t) {
  let e;
  return L(t, (i) => e = i)(), e;
}
const p = [];
function y(t, e = k) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function l(c) {
    if (D(t, c) && (t = c, i)) {
      const u = !p.length;
      for (const f of n)
        f[1](), p.push(f, t);
      if (u) {
        for (let f = 0; f < p.length; f += 2)
          p[f][0](p[f + 1]);
        p.length = 0;
      }
    }
  }
  function s(c) {
    l(c(t));
  }
  function o(c, u = k) {
    const f = [c, u];
    return n.add(f), n.size === 1 && (i = e(l, s) || k), c(t), () => {
      n.delete(f), n.size === 0 && i && (i(), i = null);
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
  const t = y({});
  return E(Z, t);
}
const G = "$$ms-gr-antd-context-key";
function H(t) {
  var c;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = z(), i = T({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((u) => {
    i.slotKey.set(u);
  }), J();
  const n = M(G), l = ((c = g(n)) == null ? void 0 : c.as_item) || t.as_item, s = n ? l ? g(n)[l] : g(n) : {}, o = y({
    ...t,
    ...s
  });
  return n ? (n.subscribe((u) => {
    const {
      as_item: f
    } = g(o);
    f && (u = u[f]), o.update((_) => ({
      ..._,
      ...u
    }));
  }), [o, (u) => {
    const f = u.as_item ? g(n)[u.as_item] : g(n);
    return o.set({
      ...u,
      ...f
    });
  }]) : [o, (u) => {
    o.set(u);
  }];
}
const V = "$$ms-gr-antd-slot-key";
function J() {
  E(V, y(void 0));
}
function z() {
  return M(V);
}
const Q = "$$ms-gr-antd-component-slot-context-key";
function T({
  slot: t,
  index: e,
  subIndex: i
}) {
  return E(Q, {
    slotKey: y(t),
    slotIndex: y(e),
    subSlotIndex: y(i)
  });
}
function W(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var R = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
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
        e.call(s, c) && s[c] && (o = l(o, c));
      return o;
    }
    function l(s, o) {
      return o ? s ? s + " " + o : s + o : s;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(R);
var $ = R.exports;
const ee = /* @__PURE__ */ W($), {
  getContext: te,
  setContext: ne
} = window.__gradio__svelte__internal;
function se(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function i(l = ["default"]) {
    const s = l.reduce((o, c) => (o[c] = y([]), o), {});
    return ne(e, {
      itemsMap: s,
      allowedSlots: l
    }), s;
  }
  function n() {
    const {
      itemsMap: l,
      allowedSlots: s
    } = te(e);
    return function(o, c, u) {
      l && (o ? l[o].update((f) => {
        const _ = [...f];
        return s.includes(o) ? _[c] = u : _[c] = void 0, _;
      }) : s.includes("default") && l.default.update((f) => {
        const _ = [...f];
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
  getItems: ie,
  getSetItemFn: le
} = se("cascader"), {
  SvelteComponent: oe,
  check_outros: re,
  component_subscribe: x,
  create_slot: ce,
  detach: ue,
  empty: ae,
  flush: d,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: de,
  insert: be,
  safe_not_equal: ye,
  transition_in: j,
  transition_out: P,
  update_slot_base: he
} = window.__gradio__svelte__internal;
function F(t) {
  let e;
  const i = (
    /*#slots*/
    t[21].default
  ), n = ce(
    i,
    t,
    /*$$scope*/
    t[20],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(l, s) {
      n && n.m(l, s), e = !0;
    },
    p(l, s) {
      n && n.p && (!e || s & /*$$scope*/
      1048576) && he(
        n,
        i,
        l,
        /*$$scope*/
        l[20],
        e ? _e(
          i,
          /*$$scope*/
          l[20],
          s,
          null
        ) : fe(
          /*$$scope*/
          l[20]
        ),
        null
      );
    },
    i(l) {
      e || (j(n, l), e = !0);
    },
    o(l) {
      P(n, l), e = !1;
    },
    d(l) {
      n && n.d(l);
    }
  };
}
function ge(t) {
  let e, i, n = (
    /*$mergedProps*/
    t[0].visible && F(t)
  );
  return {
    c() {
      n && n.c(), e = ae();
    },
    m(l, s) {
      n && n.m(l, s), be(l, e, s), i = !0;
    },
    p(l, [s]) {
      /*$mergedProps*/
      l[0].visible ? n ? (n.p(l, s), s & /*$mergedProps*/
      1 && j(n, 1)) : (n = F(l), n.c(), j(n, 1), n.m(e.parentNode, e)) : n && (me(), P(n, 1, 1, () => {
        n = null;
      }), re());
    },
    i(l) {
      i || (j(n), i = !0);
    },
    o(l) {
      P(n), i = !1;
    },
    d(l) {
      l && ue(e), n && n.d(l);
    }
  };
}
function pe(t, e, i) {
  let n, l, s, o, c, {
    $$slots: u = {},
    $$scope: f
  } = e, {
    gradio: _
  } = e, {
    props: m = {}
  } = e;
  const b = y(m);
  x(t, b, (r) => i(19, c = r));
  let {
    _internal: a = {}
  } = e, {
    value: h
  } = e, {
    label: C
  } = e, {
    as_item: K
  } = e, {
    visible: S = !0
  } = e, {
    elem_id: v = ""
  } = e, {
    elem_classes: w = []
  } = e, {
    elem_style: I = {}
  } = e;
  const N = z();
  x(t, N, (r) => i(18, o = r));
  const [O, U] = H({
    gradio: _,
    props: c,
    _internal: a,
    visible: S,
    elem_id: v,
    elem_classes: w,
    elem_style: I,
    as_item: K,
    value: h,
    label: C
  });
  x(t, O, (r) => i(0, s = r));
  const q = B();
  x(t, q, (r) => i(17, l = r));
  const X = le(), {
    default: A
  } = ie();
  return x(t, A, (r) => i(16, n = r)), t.$$set = (r) => {
    "gradio" in r && i(6, _ = r.gradio), "props" in r && i(7, m = r.props), "_internal" in r && i(8, a = r._internal), "value" in r && i(9, h = r.value), "label" in r && i(10, C = r.label), "as_item" in r && i(11, K = r.as_item), "visible" in r && i(12, S = r.visible), "elem_id" in r && i(13, v = r.elem_id), "elem_classes" in r && i(14, w = r.elem_classes), "elem_style" in r && i(15, I = r.elem_style), "$$scope" in r && i(20, f = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    128 && b.update((r) => ({
      ...r,
      ...m
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, label*/
    589632 && U({
      gradio: _,
      props: c,
      _internal: a,
      visible: S,
      elem_id: v,
      elem_classes: w,
      elem_style: I,
      as_item: K,
      value: h,
      label: C
    }), t.$$.dirty & /*$slotKey, $mergedProps, $slots, $items*/
    458753 && X(o, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: ee(s.elem_classes, "ms-gr-antd-cascader-option"),
        id: s.elem_id,
        label: s.label,
        value: s.value,
        ...s.props,
        ...Y(s)
      },
      slots: l,
      children: n.length > 0 ? n : void 0
    });
  }, [s, b, N, O, q, A, _, m, a, h, C, K, S, v, w, I, n, l, o, c, f, u];
}
class xe extends oe {
  constructor(e) {
    super(), de(this, e, pe, ge, ye, {
      gradio: 6,
      props: 7,
      _internal: 8,
      value: 9,
      label: 10,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), d();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(e) {
    this.$$set({
      props: e
    }), d();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), d();
  }
  get value() {
    return this.$$.ctx[9];
  }
  set value(e) {
    this.$$set({
      value: e
    }), d();
  }
  get label() {
    return this.$$.ctx[10];
  }
  set label(e) {
    this.$$set({
      label: e
    }), d();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), d();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), d();
  }
}
export {
  xe as default
};
