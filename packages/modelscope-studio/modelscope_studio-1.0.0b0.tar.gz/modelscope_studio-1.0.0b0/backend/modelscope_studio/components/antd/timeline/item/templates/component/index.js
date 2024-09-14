function D(n) {
  const {
    gradio: t,
    _internal: s,
    ...i
  } = n;
  return Object.keys(s).reduce((o, e) => {
    const l = e.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], u = c.split("_"), _ = (...m) => {
        const b = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
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
          payload: b,
          component: i
        });
      };
      if (u.length > 1) {
        let m = {
          ...i.props[u[0]] || {}
        };
        o[u[0]] = m;
        for (let f = 1; f < u.length - 1; f++) {
          const p = {
            ...i.props[u[f]] || {}
          };
          m[u[f]] = p, m = p;
        }
        const b = u[u.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = _, o;
      }
      const a = u[0];
      o[`on${a.slice(0, 1).toUpperCase()}${a.slice(1)}`] = _;
    }
    return o;
  }, {});
}
function v() {
}
function L(n, t) {
  return n != n ? t == t : n !== t || n && typeof n == "object" || typeof n == "function";
}
function Z(n, ...t) {
  if (n == null) {
    for (const i of t)
      i(void 0);
    return v;
  }
  const s = n.subscribe(...t);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function h(n) {
  let t;
  return Z(n, (s) => t = s)(), t;
}
const g = [];
function d(n, t = v) {
  let s;
  const i = /* @__PURE__ */ new Set();
  function o(c) {
    if (L(n, c) && (n = c, s)) {
      const u = !g.length;
      for (const _ of i)
        _[1](), g.push(_, n);
      if (u) {
        for (let _ = 0; _ < g.length; _ += 2)
          g[_][0](g[_ + 1]);
        g.length = 0;
      }
    }
  }
  function e(c) {
    o(c(n));
  }
  function l(c, u = v) {
    const _ = [c, u];
    return i.add(_), i.size === 1 && (s = t(o, e) || v), c(n), () => {
      i.delete(_), i.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: o,
    update: e,
    subscribe: l
  };
}
const {
  getContext: A,
  setContext: P
} = window.__gradio__svelte__internal, B = "$$ms-gr-antd-slots-key";
function G() {
  const n = d({});
  return P(B, n);
}
const H = "$$ms-gr-antd-context-key";
function J(n) {
  var c;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = M(), s = W({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  t && t.subscribe((u) => {
    s.slotKey.set(u);
  }), Q();
  const i = A(H), o = ((c = h(i)) == null ? void 0 : c.as_item) || n.as_item, e = i ? o ? h(i)[o] : h(i) : {}, l = d({
    ...n,
    ...e
  });
  return i ? (i.subscribe((u) => {
    const {
      as_item: _
    } = h(l);
    _ && (u = u[_]), l.update((a) => ({
      ...a,
      ...u
    }));
  }), [l, (u) => {
    const _ = u.as_item ? h(i)[u.as_item] : h(i);
    return l.set({
      ...u,
      ..._
    });
  }]) : [l, (u) => {
    l.set(u);
  }];
}
const F = "$$ms-gr-antd-slot-key";
function Q() {
  P(F, d(void 0));
}
function M() {
  return A(F);
}
const T = "$$ms-gr-antd-component-slot-context-key";
function W({
  slot: n,
  index: t,
  subIndex: s
}) {
  return P(T, {
    slotKey: d(n),
    slotIndex: d(t),
    subSlotIndex: d(s)
  });
}
function $(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
}
var V = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(n) {
  (function() {
    var t = {}.hasOwnProperty;
    function s() {
      for (var e = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
        c && (e = o(e, i(c)));
      }
      return e;
    }
    function i(e) {
      if (typeof e == "string" || typeof e == "number")
        return e;
      if (typeof e != "object")
        return "";
      if (Array.isArray(e))
        return s.apply(null, e);
      if (e.toString !== Object.prototype.toString && !e.toString.toString().includes("[native code]"))
        return e.toString();
      var l = "";
      for (var c in e)
        t.call(e, c) && e[c] && (l = o(l, c));
      return l;
    }
    function o(e, l) {
      return l ? e ? e + " " + l : e + l : e;
    }
    n.exports ? (s.default = s, n.exports = s) : window.classNames = s;
  })();
})(V);
var tt = V.exports;
const et = /* @__PURE__ */ $(tt), {
  getContext: nt,
  setContext: st
} = window.__gradio__svelte__internal;
function it(n) {
  const t = `$$ms-gr-antd-${n}-context-key`;
  function s(o = ["default"]) {
    const e = o.reduce((l, c) => (l[c] = d([]), l), {});
    return st(t, {
      itemsMap: e,
      allowedSlots: o
    }), e;
  }
  function i() {
    const {
      itemsMap: o,
      allowedSlots: e
    } = nt(t);
    return function(l, c, u) {
      o && (l ? o[l].update((_) => {
        const a = [..._];
        return e.includes(l) ? a[c] = u : a[c] = void 0, a;
      }) : e.includes("default") && o.default.update((_) => {
        const a = [..._];
        return a[c] = u, a;
      }));
    };
  }
  return {
    getItems: s,
    getSetItemFn: i
  };
}
const {
  getItems: Ct,
  getSetItemFn: ot
} = it("timeline"), {
  SvelteComponent: lt,
  binding_callbacks: rt,
  check_outros: ct,
  component_subscribe: x,
  create_slot: ut,
  detach: z,
  element: ft,
  empty: _t,
  flush: y,
  get_all_dirty_from_scope: at,
  get_slot_changes: mt,
  group_outros: dt,
  init: bt,
  insert: R,
  safe_not_equal: yt,
  set_custom_element_data: pt,
  transition_in: I,
  transition_out: j,
  update_slot_base: ht
} = window.__gradio__svelte__internal;
function q(n) {
  let t, s;
  const i = (
    /*#slots*/
    n[19].default
  ), o = ut(
    i,
    n,
    /*$$scope*/
    n[18],
    null
  );
  return {
    c() {
      t = ft("svelte-slot"), o && o.c(), pt(t, "class", "svelte-8w4ot5");
    },
    m(e, l) {
      R(e, t, l), o && o.m(t, null), n[20](t), s = !0;
    },
    p(e, l) {
      o && o.p && (!s || l & /*$$scope*/
      262144) && ht(
        o,
        i,
        e,
        /*$$scope*/
        e[18],
        s ? mt(
          i,
          /*$$scope*/
          e[18],
          l,
          null
        ) : at(
          /*$$scope*/
          e[18]
        ),
        null
      );
    },
    i(e) {
      s || (I(o, e), s = !0);
    },
    o(e) {
      j(o, e), s = !1;
    },
    d(e) {
      e && z(t), o && o.d(e), n[20](null);
    }
  };
}
function gt(n) {
  let t, s, i = (
    /*$mergedProps*/
    n[1].visible && q(n)
  );
  return {
    c() {
      i && i.c(), t = _t();
    },
    m(o, e) {
      i && i.m(o, e), R(o, t, e), s = !0;
    },
    p(o, [e]) {
      /*$mergedProps*/
      o[1].visible ? i ? (i.p(o, e), e & /*$mergedProps*/
      2 && I(i, 1)) : (i = q(o), i.c(), I(i, 1), i.m(t.parentNode, t)) : i && (dt(), j(i, 1, 1, () => {
        i = null;
      }), ct());
    },
    i(o) {
      s || (I(i), s = !0);
    },
    o(o) {
      j(i), s = !1;
    },
    d(o) {
      o && z(t), i && i.d(o);
    }
  };
}
function xt(n, t, s) {
  let i, o, e, l, c, {
    $$slots: u = {},
    $$scope: _
  } = t, {
    gradio: a
  } = t, {
    props: m = {}
  } = t;
  const b = d(m);
  x(n, b, (r) => s(17, c = r));
  let {
    _internal: f = {}
  } = t, {
    as_item: p
  } = t, {
    visible: C = !0
  } = t, {
    elem_id: K = ""
  } = t, {
    elem_classes: S = []
  } = t, {
    elem_style: w = {}
  } = t;
  const k = d();
  x(n, k, (r) => s(0, o = r));
  const E = M();
  x(n, E, (r) => s(16, l = r));
  const [N, U] = J({
    gradio: a,
    props: c,
    _internal: f,
    visible: C,
    elem_id: K,
    elem_classes: S,
    elem_style: w,
    as_item: p
  });
  x(n, N, (r) => s(1, e = r));
  const O = G();
  x(n, O, (r) => s(15, i = r));
  const X = ot();
  function Y(r) {
    rt[r ? "unshift" : "push"](() => {
      o = r, k.set(o);
    });
  }
  return n.$$set = (r) => {
    "gradio" in r && s(7, a = r.gradio), "props" in r && s(8, m = r.props), "_internal" in r && s(9, f = r._internal), "as_item" in r && s(10, p = r.as_item), "visible" in r && s(11, C = r.visible), "elem_id" in r && s(12, K = r.elem_id), "elem_classes" in r && s(13, S = r.elem_classes), "elem_style" in r && s(14, w = r.elem_style), "$$scope" in r && s(18, _ = r.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*props*/
    256 && b.update((r) => ({
      ...r,
      ...m
    })), n.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    163456 && U({
      gradio: a,
      props: c,
      _internal: f,
      visible: C,
      elem_id: K,
      elem_classes: S,
      elem_style: w,
      as_item: p
    }), n.$$.dirty & /*$slotKey, $mergedProps, $slot, $slots*/
    98307 && X(l, e._internal.index || 0, {
      props: {
        style: e.elem_style,
        className: et(e.elem_classes, "ms-gr-antd-timeline-item"),
        id: e.elem_id,
        ...e.props,
        ...D(e)
      },
      slots: {
        children: o,
        ...i
      }
    });
  }, [o, e, b, k, E, N, O, a, m, f, p, C, K, S, w, i, l, c, _, u, Y];
}
class Kt extends lt {
  constructor(t) {
    super(), bt(this, t, xt, gt, yt, {
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), y();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), y();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), y();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), y();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), y();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), y();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), y();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), y();
  }
}
export {
  Kt as default
};
